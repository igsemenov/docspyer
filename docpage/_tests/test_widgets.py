# -*- coding: utf-8 -*-
"""Test widgets for the docpage template.
"""

from docspyer.docpage import widgets


def send_images(contents, bookmark, homepage):

    images = [
        f'const imageContents = `{contents}`;',
        f'const imageBookmark = `{bookmark}`;',
        f'const imageHomepage = `{homepage}`;'
    ]

    script = '\n'.join(images)

    with open('_images.js', encoding='utf-8', mode='w') as file:
        file.write(script)


if __name__ == '__main__':

    contents_ = widgets.Contents().maketag(width=300, height=300)
    bookmark_ = widgets.Bookmark().maketag(width=300, height=300)
    homepage_ = widgets.Homepage().maketag(width=360, height=300)

    send_images(
        contents_, bookmark_, homepage_
    )
