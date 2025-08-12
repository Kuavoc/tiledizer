Before and after

<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/8b9836c6-ec89-44b0-95c4-9c675b0c17ba" />
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/0aa55ba7-d86d-4eec-bc09-2aea10a43f31" />

Example A4 page


<img width="602" height="851" alt="Example page" src="https://github.com/user-attachments/assets/eabf8cbe-383b-49ac-add1-76969fb5e327" />


# tiledizer
Tiles images to Letter or A4 format and converts to PDF for printing, cutting and assembling, made with sewing patterns created in [Seamly2D](https://github.com/fashionfreedom/seamly2d) in mind, specifically exported Seamly2D pieces in .png format, as they have a consistent 96 DPI, that works for calculating an accurate final size for the pages that matches the size in milimeters of Letter and A4 pages, may work with other dpi sizes but not tested.

Final .pdf has these masurements with a 96 DPI image:

+ Letter: 215.9 x 279.4 mm
+ A4: 210.079 x 297.127 mm (Not exactly accurate, A4 is 210 x 297 mm)

### Requirements
+ Python>=3.8
+ Pillow>=10.4.0

### Use
Execute tiledizer.py and input requested parameters.

<img width="614" height="129" alt="image" src="https://github.com/user-attachments/assets/e6a1764e-431b-47a2-ac43-c97f6d8b6ec2" />

### Assemble 
Print and cut the margins only on the marked sides, tape or glue over the not cut margins.

The letters correspond to the rows, so: 

+ First row: A1, A2, A3, A4 
+ Second row: B1, B2, B3, B4
+ Third row: C1, C2, C3, C4
+ And so on...

So assembling would go kind of like this:

+ Place A1 (no cutting)
+ Cut margin on the left of A2 and glue/tape on the margin of A1 (making sure lines in the pattern and tne top and bottom of the page match)
+ Cut margin on the left of A3 and glue/tape on the margin of A2, in the same way as before
+ Cut margin on the left of the rest of the tiles of the first row and glue/tape like before
+ Cut margin on the top of B1 and glue/tape the top of B1 on the bottom margin of A1
+ Cut margin on the top and left of B2 and glue/tape it to the right margin of B1 and bottom margin of A2, a lot like tje first row
+ Cut and glue/tape every row until no tiles are left

### How to export pieces in Seamly2D
+ Open a pattern with created pieces in [Seamly2D](https://github.com/fashionfreedom/seamly2d)
+ Go to "Piece Mode"

   <img width="198" height="55" alt="image" src="https://github.com/user-attachments/assets/d1a43e0e-3793-41bf-8bbc-00f193126260" />
+ While in "Piece Mode" go to "Tools > Details > Export Pieces"

  <img width="385" height="301" alt="image" src="https://github.com/user-attachments/assets/eb6555f5-f2af-4be3-87b6-3930493933b2" />
+ Save pieces as a .png (recommended for this script)

   <img width="762" height="431" alt="image" src="https://github.com/user-attachments/assets/7bd95e94-4938-4033-abe2-6d6f9aa687e6" />
+ ! Remember to include the desired pieces before exporting

  <img width="285" height="165" alt="image" src="https://github.com/user-attachments/assets/0d9cf1c7-8136-4f50-9a6d-db1af3b67a6e" />

! Has only been tested on Windows

