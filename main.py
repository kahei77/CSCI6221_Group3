
import os
import gradio as gr

#  removebg,changebg,repair-photo,human-cartoon,video-cartoon,ocr,cntext2image
if __name__ == '__main__':
    removebg,changebg , repairPhoto,humanCartoon= "removebg","changebg","repair-photo","human-cartoon"
    appNameDic={
        removebg: "Remove Background",
        changebg:"Change Background",
        repairPhoto:"Repair Old-photo",
        humanCartoon: "Stylelish Picture",
    }
    types = os.getenv('types','removebg,changebg')
    concurrency_count = os.getenv("queue",2)


    print("active types="+types)

    actives = types.split(",")


    appNameList = []
    appList = []
    for appKey in actives:
        if appNameDic[appKey]:
            print("Activate Application:"+appNameDic[appKey])
            appNameList.append(appNameDic[appKey])
        if appKey == removebg:
            from pages.removebg import removeBgApplication
            appList.append(removeBgApplication)
        if appKey == changebg:
            from pages.changebg import changeBgApp
            appList.append(changeBgApp)
        if appKey == humanCartoon:
            from pages.humancartoon import humanCartoonApp
            appList.append(humanCartoonApp)
        if appKey == repairPhoto:
            from pages.photorepair import photoRepairApp
            appList.append(photoRepairApp)

    app = gr.TabbedInterface(appList,appNameList)
    app.queue(concurrency_count=concurrency_count).launch(server_name="0.0.0.0")
