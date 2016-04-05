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

    Due to we created some helpers scripts ese sudo is a good idea, but you can replace sud by --user
Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv vxscreenshots
    $ pip install vxscreenshots
