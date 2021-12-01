import CompareImg as compare
imgKpath = '51GCzHHt6DL._AC_SX522_.jpg'
imgHpath = '51GCzHHt6DL._AC_SX522_2.jpg'
compare_image = compare.CompareImage(imgKpath, imgHpath)
image_difference = compare_image.compare_image()
