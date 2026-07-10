
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Top 500 Albums of All Time</title>
    <link rel="stylesheet" href="p2styles.css">
  </head>

  <body>
    <nav>
      <ul>
        <li><a href="index.html" class="navlink">Home</a></li>
        <li class="current"><a href="index.py" class="navlink">Top 500 Albums Chart</a></li>
        <li><a href="makegraphs.py" class="navlink">Graphing</a></li>
      </ul>
    </nav>
    <h1>Top 500 Albums of All Time</h1>
    <h2>All data from <a href="https://rateyourmusic.com/charts/top/album/all-time/">RYM</a></h2>
    
    <form action="" method="GET" style="margin-bottom: 20px;">
        <label for="searchtype">Filter by </label>
        <select id="searchtype" name="type" style="margin-right: 5px;">
            <option value="artist" >Artist</option>
            <option value="year" >Year/Decade</option>
            <option value="genre" selected>Genre</option>
        </select>
        <input type="text" id="search" name="keyword" value="" placeholder="e.g. rock, rap...">
        <input type="submit" value="Search">
        <a href="./index.py" style="margin-left: 10px;">Clear</a>
    </form>

  </body>
</html>
