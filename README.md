Spotify Big Picture
=================

This Python script modifies Spotify *skin.xml* to create larger fonts in the Spotify client.

It is mostly useful if Spotify is being used on a larger screen such as a TV with high resolution, 
which results in very small fonts in the Spotify client.

# Executing the script

Make sure Spotify is **not** running and then execute the following command:

###Linux
```
> sudo python spotifyBigPicture.py
```

###OS X (Not tested)
```
> python spotifyBigPicture.py
```

###Windows
```
> python spotifyBigPicture.py
```

# Restore changes

If after executing the script you realize this was not what you wanted you can restore to the default font size by doing the following:

## Linux

Go to **/opt/spotify/spotify-client/Data** and replace *resources.zip* with *resources.zip.bak*

## OS X

Go to **/Applications/Spotify.app/Contents/Resources/** and replace *skin.xml* with *skin.xml.bak*

## Windows

Go to **[Spotify installation directory]\Data\** and replace *resources.zip* with *resources.zip.bak*

the installation directory for Spotify should be similar to **C:\Program Files (x86)\Spotify**
