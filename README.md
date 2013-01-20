Python twitter bot for @melty\_blood\_bot
====================

Bot account: [@melty_blood_bot](https://twitter.com/melty_blood_bot)

Installation
---------------------

Clone from http://github.com/yonchu/twitter_melty_blood_bot
and install it with::

```console
$ git clone git://github.com/yonchu/twitter_bot.git
$ git submodule update --init
$ git submodule foreach "git checkout master"
```

Usage
---------------------

Create your ``bot.cfg`` file.

```console
$ cd config
$ cp bot.cfg.sample bot.cfg
```

Edit ``bot.cfg`` to suite your environments.

Initialize.

```console
$ ./melty_blood_bot.py init
```

Run ``melty_blood_bot.py`` using run-script in cron.

```
run-script/run-script start ./melty_blood_bot.py
```
