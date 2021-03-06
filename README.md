[![version][pypi-version]][pypi-url]

[![License][pypi-license]][license-url]
[![Downloads][pypi-downloads]][pypi-url]


About
=====

articleDateExtract (Article Date Extract) is a simple open source Python module which is an extension of the [articleDateExtracor](https://pypi.org/project/articleDateExtractor/), built and maintained by [Krishna Kishore](https://webruster.tk), that automatically detects, extracts and normalizes the publication date of an online article or blog post.

## Feature


1.  Extracting the publication date information when it is specified in a web page, with over 95% success rate.


## A Quick Example


```python

    import articleDateExtract

    d = articleDateExtract.extractArticlePublishedDate("http://edition.cnn.com/2015/11/28/opinions/sutter-cop21-paris-preview-two-degrees/index.html")

    print (d)

    d = articleDateExtract.extractArticlePublishedDate("http://techcrunch.com/2015/11/29/tyro-payments/")

    print (d)

```


## Installing

Available through pip:

```bash

    $ pip install articleDateExtract
```
Alternatively, you can install from source:

```bash

    $ git clone https://github.com/blueshirtdeveloper/article-date-extract.git
    $ cd article-date-extract
    $ python setup.py install
```

## Dependencies

* [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/bs4/) >= 4.9.3
* [python-dateutil](https://github.com/dateutil/dateutil/) >= 2.7.3
* [lxml](lxml.de) >= 4.6.1


## About Krishna Kishore


I'm Krishna Kishore. I work as a full-time programmer. In my spare time I do open-sourcing. we crawl the news sites so the need for a scalable solution that will automatically extract and structure the unstructured web is critical. We use multiple signals and algorithms to automatically detect where the post text is, the author name, the comments,
and of course the date. With articleDateExtract (Article Date Extract) we rely on the many "different types of standards" out there to automatically detect the date (with a success rate of over 95%).




[license-url]: https://github.com/blueshirtdeveloper/article-date-extract/blob/main/LICENSE



[pypi-url]: https://pypi.python.org/pypi/articleDateExtract
[pypi-license]: https://img.shields.io/pypi/l/articleDateExtract.svg
[pypi-version]: https://img.shields.io/pypi/v/articleDateExtract.svg?style=flat
[pypi-downloads]: https://img.shields.io/pypi/dm/articleDateExtract.svg?style=flat
