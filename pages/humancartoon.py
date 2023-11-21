import gradio as gr
from modelscope.outputs import OutputKeys
from commonutils import ImageUtils
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# AI绘画 卡通
print("loading cartoon model")
img_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon_compound-models')
print("loading cartoon model-sketch")
img_sketch_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon-sketch_compound-models')
print("loading cartoon model-3d")
img_3d_cartoon = pipeline(Tasks.image_portrait_stylization,model='damo/cv_unet_person-image-cartoon-3d_compound-models')
print("loading cartoon model-art")
img_artstyle_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon-artstyle_compound-models')
print("loading cartoon model-hand-drawn")
img_handdrawn_cartoon = pipeline(Tasks.image_portrait_stylization, model='damo/cv_unet_person-image-cartoon-handdrawn_compound-models')

with gr.Blocks(title="Image stylization", css="#fixed_size_img {height: 240px;} ") as humanCartoonApp:
    style_dict = {"anime": "anime", "3d": "3d", "handdrawn": "handdrawn", "sketch": "sketch", "artstyle": "artstyle"}
    def inference(image, style) :

        style = style_dict[style]
        print("sytle=" + style)
        if style == "anime":
            image = img_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "3d":
            image = img_3d_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "handdrawn":
            image = img_handdrawn_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "sketch":
            image = img_sketch_cartoon(image)[OutputKeys.OUTPUT_IMG]
        if style == "artstyle":
            image = img_artstyle_cartoon(image)[OutputKeys.OUTPUT_IMG]
        return ImageUtils.imageOutput(image)

    gr.HTML('''
          <div style="text-align: center; max-width: 720px; margin: 0 auto;">
                      <div
                        style="
                          display: inline-flex;
                          align-items: center;
                          gap: 0.8rem;
                          font-size: 1.75rem;
                        "
                      >
                        <h1 style="font-family:  PingFangSC; font-weight: 500; line-height: 1.5em; font-size: 32px; margin-bottom: 7px;">
                          Image stylization
                        </h1>
                      </div>
                      <img id="overview" alt="overview" src="https://modelscope.oss-cn-beijing.aliyuncs.com/demo/image-cartoon/demo_sin1.gif" />

                    </div>
          ''')
    gr.Markdown("Upload any photo you like, whether it's street photography, portraits, or group shots. Choose a style that suits your taste.")
    with gr.Row():
        radio_style = gr.Radio(label="style choice", choices=["anime", "3d", "handdrawn", "sketch", "artstyle"],
                               value="anime")
    with gr.Row():
        img_input = gr.Image(type="pil", elem_id="fixed_size_img")
        img_output = gr.Image(type="pil", elem_id="fixed_size_img")
    with gr.Row():
        btn_submit = gr.Button(value="create new picture", elem_id="blue_btn")
    examples = gr.Examples(examples= [['./images/examples/humancartoon1.png'], ['./images/examples/humancartoon2.png'], ['./images/examples/humancartoon3.png']], inputs=[img_input], outputs=img_output)
    btn_submit.click(inference, inputs=[img_input, radio_style], outputs=img_output)