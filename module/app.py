import streamlit as st
from PIL import Image, ImageOps
import os
# from reportlab.pdfgen import canvas


def images_to_pdf(image_list, output_filename):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(output_filename)
    for i, image_path in enumerate(image_list):  
        image = Image.open(image_path)
        
        image = ImageOps.exif_transpose(image)
        width, height = image.size
        c.setPageSize((width, height))
        
        temp_image_path = f"temp_image_{i}.jpg"
        image.save(temp_image_path)
        
        c.drawImage(temp_image_path, 0, 0, width=width, height=height)
        c.showPage()

        os.remove(temp_image_path)
    c.save()

def find_similar_images(folder_path):
    similar_groups = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            prefix = filename[:12]  
            if prefix in similar_groups:
                similar_groups[prefix].append(os.path.join(folder_path, filename))
            else:
                similar_groups[prefix] = [os.path.join(folder_path, filename)]
    return similar_groups

def main(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    similar_groups = find_similar_images(source_folder)
    for group_name, image_paths in similar_groups.items():
        if len(image_paths) > 1:  
            output_filename = os.path.join(target_folder, f'{group_name}.pdf')
            images_to_pdf(image_paths, output_filename)
            # print(f'Created PDF with {len(image_paths)} pages: {output_filename}')
            st.write(f'Created PDF with {len(image_paths)} pages: {output_filename}')
        else:
            # print(f'No similar images to merge for prefix {group_name}')
            st.write(f'No similar images to merge for prefix {group_name}')



if __name__ == '__main__':
    # 页面配置
    st.set_page_config(page_title="函证图片合并工具", page_icon="🔧", layout="wide")
    st.title("函证图片合并工具")

    source_folder = st.text_input("请输入【函证下载】文件夹路径:")
    target_folder = st.text_input("请输入【结果】文件夹路径:")
    if st.button("执行"):
        main(source_folder, target_folder)



