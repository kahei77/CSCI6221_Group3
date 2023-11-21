import gradio as gr
from modelscope.outputs import OutputKeys
from commonutils import ImageUtils
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
#image-portrait-enhancement
print("loading image-portrait-enhancement")
portrait_enhancement = pipeline(Tasks.image_portrait_enhancement, model='damo/cv_gpen_image-portrait-enhancement')

#image-colorization
# img_colorization = pipeline(Tasks.image_colorization,  model='damo/cv_ddcolor_image-colorization')


# image-denoising
print("loading image-denoise model")
image_denoise_pipeline = pipeline(Tasks.image_denoising, model='damo/cv_nafnet_image-denoise_sidd')


# image-color-enhancement
print("loading image-color-enhance-models")
image_color_enhance = pipeline(Tasks.image_color_enhancement, model='damo/cv_csrnet_image-color-enhance-models')

with gr.Blocks(title="photo repair", css="#overview {margin: auto;max-width: 600px; max-height: 400px; width: 100%;}") as photoRepairApp:
    yes, no = "yes", "no"
    def inference(img, image_denoise_option, color_enhance_option,progress=gr.Progress()) :
        step = 1
        if image_denoise_option == yes:
            step += 1
        if color_enhance_option == yes:
            step += 1
        echoStep = 1.0/step
        startPrecent = 0
        # 人像修复
        progress(startPrecent, desc="image  fixing.....")
        img = portrait_enhancement(img)[OutputKeys.OUTPUT_IMG]



        # 图像上色
        # if colorization_optio == yes:
        #     startPrecent += echoStep
        #     progress(startPrecent, desc="正在进行图像上色.....")
        #     img = img_colorization(img)[OutputKeys.OUTPUT_IMG]
        # 图像去噪
        if image_denoise_option == yes:
            startPrecent += echoStep
            progress(startPrecent, desc="image denosing.....")
            img = image_denoise_pipeline(img)[OutputKeys.OUTPUT_IMG]

        # 图像调色
        if color_enhance_option ==yes:
            startPrecent += echoStep
            progress(startPrecent, desc="image enchancing.....")
            img = image_color_enhance(img)[OutputKeys.OUTPUT_IMG]


        progress(1, desc="fix ending, start coloring")
        return ImageUtils.imageOutput(img)



    examples = [['./images/examples/repair1.jpg'],
                ['./images/examples/repair2.jpg'],
                ['./images/examples/repair3.jpg'],
                ['./images/examples/repair4.jpg'],
                ['./images/examples/repair5.jpg']]

    # gr.HTML('''
    #         <div style="text-align: center; max-width: 720px; margin: 0 auto;">
    #             <img id="overview" alt="overview" src="./images/repair.gif" />
    #         </div>
    #       ''')
    gr.HTML(ImageUtils.image2HtmlTag("images/repair.gif"))
    gr.Markdown("Upload an old photo and click to restore. AI will enhance and colorize it, bringing your old pictures back to life")
    with gr.Row():
        with gr.Column(scale=2):
            img_input = gr.Image(label="Image", type="pil")
            # colorization_option = gr.Radio(label="重新上色", choices=[yes, no], value=yes)
            image_denoise_option = gr.Radio(label="Apply image denoising", choices=[yes, no],
                                                       value=no)
            color_enhance_option = gr.Radio(label="Apply color enhancement ", choices=[yes, no],
                                                       value=no)
            btn = gr.Button("repairing")
        with gr.Column(scale=3):
            img_output = gr.Image(type="pil")
    inputs = [img_input,image_denoise_option, color_enhance_option]
    btn.click(fn=inference, inputs=inputs, outputs=img_output)
    gr.Examples(examples, inputs=img_input)

