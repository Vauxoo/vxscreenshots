.. highlight:: shell

============
Installation
============


On Ubuntu:
==========

At the command line::

    $ sudo pip install python-pip

Installing last version of pip::

    $ sudo pip install pip --upgrade

Ensure you have the last version::

    $ pip --version
    pip 8.1.1 ""or greater""

Now install it from pip::

    Isolated on your user.

    $ pip install vxscreenshots --user
    $ echo "export PATH=$PATH:$HOME/.local/bin/" >> $HOME/.bashrc
    $ source $HOME/.bashrc

    or with sudo.

    $ sudo pip install vxscreenshots

Note::

    Due to we created some helpers scripts ese sudo is a good idea, but you can
    replace sud by --user


Testing what you just installed::

    $ vxssicon

    This should run normally.

    $ vxsswatcher

    This should run normally.

**Configuring**

First set the folder you want to supervise in the **supervised** entry on the
config file, the folder name should be you linux user in order to have some kid
of order but if you use this in several machines at once it can be usefull set
it manually also, the bucket is the name of the bucket itself configuring with
a proper DNS entry in order to set the link properlly when sharing.::

    $ vim $HOME/.vxscreenshots/vxsscreenshots.ini

Ensure your credentials to amazon are setted correctly::

    $ vim $HOME/.aws/credentials

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv vxscreenshots
    $ pip install vxscreenshots
