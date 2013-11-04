# How to use Wired Blogs
## Intro
This short guide will explain how to use the example called "wired_blogs.py" that will call the URL to make fake votes.

## Requirements
To use that script is important that the *torquey* module is installed on your machine or on the environment in use. To install it you can use this command:

     pip install torquery

You can even download/copy the entire git repository.

     git clone https://github.com/koalalorenzo/torquery.git

and then install everything using this command

    python setup.py install

Is important that you have installed [TOR](https://www.torproject.org/) on your machine.

## Get the script
If you get the torquey library downloading the git repository, the script is inside the directory "examples". 

You can download the last version of the script using this command anyway:

    curl https://raw.github.com/koalalorenzo/torquery/master/examples/wired_blogs.py > wired_blogs.py 

## How to use
To use the script you must find a URL of a blog post on [http://wired.it/](http://wired.it/) and then decide which kind of vote to use between "wired", "tired" or "expired".

Once you have everything you need, you can run the command in this way:

    python ./wired_blogs.py METHOD URL

For example, if I want to start voting [this blog post](http://daily.wired.it/news/2013/10/31/lego-mattoncini-storia-432657.html) as tired this is the right command to use:

    python ./wired_blogs.py tired http://daily.wired.it/news/2013/10/31/lego-mattoncini-storia-432657.html

The script will start voting continuously. Every time he check via Ajax that the vote is processed correctly, but because of the web server cache, you will see changes on the website after a few minutes.