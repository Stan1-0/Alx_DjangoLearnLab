from .models import *

books.all()

Library.objects.get(name=library_name)

Author.objects.get(name=author_name)
objects.filter(author=author)

Librarian.objects.get(library=librarian)


