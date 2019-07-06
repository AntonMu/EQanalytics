#  CMP Facade Database

We present a dataset of facade images assembled at the Center for Machine Perception, which includes 600 rectified images of facades from various sources, which have been manually annotated. The facades are from different cities around the world and diverse architectural styles. 

Website: [cmp.felk.cvut.cz/~tylecr1/facade](cmp.felk.cvut.cz/~tylecr1/facade)

## Content 

CMP-extended dataset, 228 images
CMP-base dataset, 378 images
Image data: `*.jpg`
Object annotation: `*.xml`
Pixelwise labels: `*.png`
Label definition: label_names.txt
  - line format: _label_id_ _class_name_ _label_z_order_

## Documentation 

Data origin, format and processing, annotation principles for 12 classes are specified in the report on the website. 

facade 
molding
cornice
pillar
window
door
sill
blind
balcony
shop
deco
background

## Citation 

Please use the following reference to cite the dataset:
```
@INPROCEEDINGS{Tylecek13,
  author = {Radim Tyle{\v c}ek, Radim {\v S}{\' a}ra},
  title = {Spatial Pattern Templates for Recognition of Objects with Regular Structure},
  booktitle = {Proc. GCPR},
  year = {2013},
  address = {Saarbrucken, Germany},
}
```
## Contact 

Maintained by Radim Tylecek tylecr1@cmp.felk.cvut.cz
Last Update: 16.9.2013   
