Spotify Big Picture
=================

This Python script modifies Spotify *skin.xml* to create larger fonts in the Spotify client.

It is mostly useful if Spotify is being used on a larger screen such as a TV with high resolution, 
which results in very small fonts in the Spotify client.

# Requrements

Python 2.7 http://www.python.org/download/

# Executing the script

Make sure Spotify is **not** running and then execute the following command:

```
> python spotifyBigPicture.py
```
Note that for **Linux** it must be executed with *sudo*

### Restore changes

To restore Spotify to default font size execute the script with the --restore flag

```
> python spotifyBigPicture.py --restore
```

### Font size

To specify your own font size use the --size flag. 
The size specified is relative, and changes will be based on its original value and the specified value.
Negative size is also allowed, to reduce the font size.
```
> python spotifyBigPicture.py --size 10
```

The default size is *8*.
