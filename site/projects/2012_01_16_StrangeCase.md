---
category: project

title: StrangeCase
date: 2011-12-21
header: another static site generator

tags:
  - On-going project

about: >
  Another static site generator. This one uses a tree representation of your site to keep
  the implementation simple, while offering a surprising amount of power.
github: colinta/StrangeCase
---
{% extends 'layouts/project.j2' %}

{% block content %}
{% markdown2 %}

This all started when I decided to replace my crufty old wordpress site with a static site, and to have it hosted at
Github.  It made the most sense to use their really nifty program, `jekyll`, but I was distraught when I found
that even something as simple as having *projects* (as opposed to *blogs*) could throw a wrench into the whole system.

I did not like assigning a `group` or `category`, and have that meta data used to build pages, and then have those pages
interwoven again when it came to using the paginator.  “Okay,” thinks I, “I'll just write a generator to create a project
page.”  Ug.  Way too much boiler plate, judging from what I saw.  I'm used to extensions being tiny snippets (SublimeText
nailed it!), not big ol' classes.  The projects out there doing what I need take two or three classes, and it's *`Ruby`*
code, which is not my first (or second (or third)) language.

`jekyll` is good at being `jekyll`, I'm not trying to say it needs to be fixed.  It doesn't.  It just doesn't fit
my needs.

Next, I took a peek at `hyde`.  Python!  Jinja!  Sweet!  It was immediately apparent that it was going to be more difficult
to setup.  Lots of config settings, and the configs *controlled* important things, and though the site is informative, the
fact that it *requires reading* so much documentation should be a kind of flag.  Isn't this supposed to be as simple as
copying from one folder to another, with some text manipulation in between?  And then when I tried to toss in `google-prettyprint`,
the whole thing fell apart (unicode error - and it's been fixed in the most recent version).

The most important thing was that it felt very difficult to do things I thought should be very simple:

* create an index page based on the contents of a `blogs/` folder.
* create `<img />` tags for all the images in a folder of images.
* add properties to a file using YAML front matter (this one they both got right, I just imitated it)
* add meta data to a config file that is accessible in all the pages.
* nothing should have to be configured, it should "just work"

To get a taste of what I mean by "simple config", here is the `config.yaml` that powers this site (as of today, 16 Jan 2012):

<pre class="prettyprint">
deploy_path: "../githubpages"
host: http://colinta.com
meta:
  analytics: 'UA-********-1'
  title: stuff by colinta
  header: colinta
  author:
    name: Colin Thomas-Arnold
    email: colinta@gmail.com
    github: colinta
    twitter: colinta
</pre>

The only thing related to `StrangeCase`'s inner workings is `deploy_path`.  **All** the rest are just inserted into templates.

I'll illustrate how simple some of the other tasks can be by showing how `StrangeCase` treats folders of images and pages.

{% raw %}<pre class="prettyprint">
{%- for image in site.static.image.zenburn -%}
  &lt;img width=&quot;100&quot; src=&quot;{{ image.url }}&quot; /&gt;
{% endfor -%}
</pre>{% endraw %}

Outputs:

<div class="well">
<pre class="prettyprint">
{%- for image in site.static.image.zenburn -%}
  &lt;img width=&quot;100&quot; src=&quot;{{ image.url }}&quot; /&gt;
{% endfor -%}
</pre>

{% for image in site.static.image.zenburn %}
  <img width="100" src="{{ image.url }}" />
{% endfor %}
</div>

(and yes, I *really am* using the code above, I just copy &amp; pasted it here)


-------------------


So that's all it takes to iterate over a folder of assets.  How about listing the `projects/` folder?

{% raw %}<pre class="prettyprint">
{%- for project in site.projects -%}
  {{ project.title }}&lt;br/&gt;
{% endfor -%}
</pre>{% endraw %}

<div class="well">
<pre class="prettyprint">
{%- for project in site.projects -%}
  {{ project.title }}&lt;br/&gt;
{% endfor -%}
</pre>

{% for project in site.projects %}
  {{ project.title }}<br/>
{% endfor %}
</div>


-------------------


There's not much more to go over that isn't in the [README](https://colinta.github.com/StrangeCase), but here goes, since
you're still here and paying attention...

The only file that is special-cased is `index.html`.  This file does not appear in the listing above (there is a file there,
though: <http://colinta.com/projects/index.html>, if you don't believe me).  This is because index files are more of a textual
representation of the folder itself, not so much an entry *in* the folder.  I think this trade off of "special-case" vs "intuitive
feature" is a good one.

The thing that, I think, makes `StrangeCase` of the greatest benefit is that you are always, essentially, working in a tree.  And
trees are easy.  You can talk to your `parent` page, or `prev` or `next`, or your `children` if you are working with a folder.

This means that if you want to feature a blog on your home page, you just refer to it by name:

{% raw %}<pre class="prettyprint">
&lt;h1&gt;My favorite plugin is &lt;a href=&quot;{{ site.projects.move_text.url }}&quot;&gt;{{ site.projects.move_text.title }}&lt;/a&gt;.&lt;/h1&gt;
</pre>{% endraw %}

<div class="well">
<pre class="prettyprint">
&lt;h1&gt;My favorite plugin is &lt;a href=&quot;{{ site.projects.move_text.url }}&quot;&gt;{{ site.projects.move_text.title }}&lt;/a&gt;.&lt;/h1&gt;
</pre>

<h1>My favorite plugin is <a href="{{ site.projects.move_text.url }}">{{ site.projects.move_text.title }}</a>.</h1>
</div>


I did cheat a little here.  The `move_text` project file is *actually* called "2011\_12\_21\_move\_text.md", and I've renamed it to
`move_text` using a config.yaml trick that looks like this:

{% raw %}<pre class="prettyprint">
files:
  "2011_12_21_move_text": { 'name': 'move_text' }
</pre>{% endraw %}

`files:` is a special key in config.yaml.  It contains the YAML front matter for files that would otherwise have *no way* to specify it, like images.
Check out (the config file)[https://raw.github.com/colinta/StrangeCase/colinta/site/static/image/2012_01_06_ouray/config.yaml] for the Ouray pictures.
The `caption:` and `target_name:` for every image is placed in there.  I don't know why I set target_name, though... I think the images were capitalized
or called something else before.

This trick could just as easily be done in the YAML front matter, and in this case that is where I will put it.  As far as I know, there is no difference
between using the config.yaml `files:` and placing things in front matter.

Here is what the YAML front matter looks like.  Really it's no different from jekyll or hyde, so no surprises here.

{% raw %}<pre class="prettyprint">
---
category: project
name: move_text

title: MoveText
date: 2011-12-21
header: Sublime Text 2 Plugin

tags:
  - Sublime Plugins

about: Select text and drag it around, or setup a text “tunnel” to move code from one location to another.
github: colinta/SublimeMoveText
---
{% extends 'layouts/project.j2' %}
…
</pre>{% endraw %}

You have no doubt noticed that there *are* a few special variables that can go in `config.yaml` that change
things like variables names and deploy locations.  But I promise I kept them to a minimum.  Or tried to, at least.

* `name`: the name you use to reference this page from other pages
* `target_name`: the file name to use after the file is copied or rendered

And finally, the name: `StrangeCase`?  As in "The `StrangeCase` of Dr. `jekyll` and Mr. `hyde`".  Which leaves `the-of-and` if someone
wants to kill a weekend writing a static site generator.  That's how long StrangeCase took to write.  That should give *some*
indication of how simple it really is.

[README](https://colinta.github.com/StrangeCase)

{% endmarkdown2 %}
{% endblock %}
