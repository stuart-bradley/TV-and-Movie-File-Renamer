# TV and Movie File Renamer

This is a simple script designed to recursively rename movies and TV shows. It also removes files (such as text files), but keeps `.srt` subtitle files. 

The files are renamed in the following formats:

`TV Show Name - S##E##`
`Movie (Year)`

## File Structure

The script assumes the following file structure:

`\TV Shows\TV Show Name\Season ##\Episode.***`
`\Movies\Movie Name (Year)\Movie.***`

It uses this structure to correctly rename both the TV shows, and the movies.

### TV Shows

When renaming TV shows, the script grabs the `title` from the parent folder. However it grabs the the season and episode information directly from the file. It can also handle this multi-episode format:

`TV Show Name - S##E##E##E##`

### Movies

The filename for movies are renamed by copying the parent folder name. This is the standard YIFY format, and is not particularly robust. 