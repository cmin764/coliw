# CoLiW (Command Line for Web)

Brings CLI to web by executing high level mash-up commands for common services.


## Installation

Clone repository, then install Python interpreter, `virtualenv` and its wrapper:
```bash
git clone git@github.com:cmin764/coliw.git
cd coliw

sudo apt-get update && sudo apt-get install --upgrade python python-dev python-pip
sudo -H pip install -U virtualenv virtualenvwrapper
```

Set-up a vritual environment:
```bash
echo "export WORKON_HOME=~/Envs" >>~/.bashrc
source ~/.bashrc
mkdir -p $WORKON_HOME
echo "source /usr/local/bin/virtualenvwrapper.sh" >>~/.bashrc
source ~/.bashrc
mkvirtualenv coliw
deactivate
```

Install 3rd party libraries and package:
```bash
workon coliw
pip install -Ur requirements.txt
python setup.py develop
deactivate
```

Run server:
```bash
workon coliw
python run.py
```

You can also add later specific envrinonmental variables in `postactivate` file:
```bash
cat etc/postactivate >> $WORKON_HOME/coliw/bin/postactivate
```
And then run `workon` command and server using the defined variables above.

Run tests and create documentation:
```bash
workon coliw
nosetests
cd docs
make html
deactivate
```


----

* Authors:
  + Cosmin Poieana <cosmin.poieana@info.uaic.ro>
  + Corneliu Tamas <corneliu.tamas@info.uaic.ro>
* Homepage: *coming soon*
* Source: https://github.com/cmin764/coliw.git
* License: MIT
