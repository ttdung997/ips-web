<!DOCTYPE html>
<html>
  <head>
    <title>
      Simple PHP Upload Demo
    </title>
  </head>
  <body>
    <form action="ftest.php" method="post" enctype="multipart/form-data">
      <input type="file" name="file-upload" accept="image/*" required>
      <input type="submit" value="Upload File" name="submit">
    </form>
  </body>
</html>

