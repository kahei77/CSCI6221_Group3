import gradio as gr
from pages.removebg import portrait_matting
from modelscope.outputs import OutputKeys
from commonutils import  ImageUtils
import numpy as np
def inference(image, bk ,progress=gr.Progress()):
    # 一键抠图
    progress(0, desc="getting background.....")
    result = portrait_matting(image)
    res_img=ImageUtils.imageOutput(result[OutputKeys.OUTPUT_IMG])
    progress(0.5, desc="swtiching background.....")
    alpha = res_img[:, :, 3:4] / 255.0
    w, h = image.size
    bk = bk.resize((w, h))
    # combine_img = Image.alpha_composite(Image.fromarray(res_img),bk)
    combine_img = image * alpha + bk * (1 - alpha)
    combine_img = combine_img.astype(np.uint8)
    return res_img, combine_img



with gr.Blocks(title="Portrait Background Replacement", css="#fixed_size_img {height: 240px;} " \
            "#overview {margin: auto;max-width: 400px; max-height: 400px;}") as changeBgApp:
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
                        <h1 style="font-family:  PingFangSC; font-weight: 500; font-size: 36px; margin-bottom: 7px;">


                          Portrait Background Replacement
                        </h1>       
          ''')
    gr.Markdown(" inputting a portrait photo and a background image, then producing an edited image where the background of the portrait is replaced")
    with gr.Row():
        img_input1 = gr.Image(label="portrait", type="pil", elem_id="fixed_size_img")
        img_output1 = gr.Image(label="portrait output", type="pil", elem_id="fixed_size_img")
    with gr.Row():
        img_input2 = gr.Image(label="background", type="pil", elem_id="fixed_size_img")
        img_output2 = gr.Image(label="background output", type="pil", elem_id="fixed_size_img")
    with gr.Row():
        btn_submit = gr.Button(value="transformation", elem_id="blue_btn")
    examples = [['./images/examples/chagebg_input2.jpg', './images/examples/chagebg_bk1.jpg'],
                ['./images/examples/chagebg_input2.jpg', './images/examples/chagebg_bk2.jpg'],
                ['./images/examples/chagebg_input3.jpg', './images/examples/chagebg_bk3.jpg']]

    examples = gr.Examples(examples=examples, inputs=[img_input1, img_input2])
    btn_submit.click(inference, inputs=[img_input1, img_input2], outputs=[img_output1, img_output2])