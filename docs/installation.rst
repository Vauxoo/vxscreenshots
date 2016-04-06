.. highlight:: shell

============
Installation
============


On Ubuntu:
==========

At the command line::

    $ sudo apt-get install python-pip \
                           awscli

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


Now run 2 tools in order of create all configuration files.::

    $ vxssicon

    This should run normally ctrl+c to kill it.

    $ vxsswatcher

    This should run normally ctrl+c to kill it.

Checking your config setted::

    $ vim ~/.vxscreenshots/vxscreenshots.ini

**Now we need to set Amazon S3 Credenetials**.

Before make a first example we need to set amazon credentials as boto3
configuration `indicates`_. And set your parameters for bucket and local
directories to be watched.::

    $ aws configure
    AWS Access Key ID [None]: YOURKEY_ID
    AWS Secret Access Key [None]: YOURKEYASKEDTOAMAZON
    Default region name [None]: us-east-1
    Default output format [None]:  

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

.. _indicates: http://boto3.readthedocs.org/en/latest/guide/configuration.html#shared-credentials-file

