# LabelImg
Using Flask to filter image

# Notes

- 将数据集文件夹放到`static`目录下，例如`static/NCP/001/666/*.jpg`
- 左右键控制读取顺序，每次会展示一个scan的所有图片
- 也可以在最上面的输入框内输入指定index
- 回车键跳转


# Structures

- static
  - NCP
    - patient_id0
      - scan_id0
        - img0.jpg
        - ...
      - scan_id1
      - ...
    - patient_id1
    - ...
- templates
  - index.html
- main.py

# Demo

![](./demo.jpg)