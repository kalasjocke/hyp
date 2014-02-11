import os
import sys

from factories import post, post_factory, comment, comment_factory

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))
