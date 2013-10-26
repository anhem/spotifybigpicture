Spotify Big Picture
=================

This Python script modifies Spotify resources to create larger fonts in Spotify desktop client.

It is mostly useful if Spotify is being used on a larger screen such as a TV with high resolution, 
which results in very small fonts in the Spotify client.

A backup is created before modifying any files, 
and the script supports restoring any changes it has made to Spotify (see **Restore changes** below)

# Requirements

* Python 2.7 - http://www.python.org/download/
* **Linux**, **OS X** or **Windows**

# Executing the script

Make sure Spotify is **not** running and then execute the following command:

```
> python spotifyBigPicture.py
```
Note that for **Linux** it must be executed with *sudo*

Executing the script several times in a row will result in larger and larger fonts.
For convenience you may instead specify the font size you want (see **Font size** below). 

It is recommended to restore the font size to its default value (see **Restore changes** below) 
before executing the script with a new font size.

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

The default size is **8**.
