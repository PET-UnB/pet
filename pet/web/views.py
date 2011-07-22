from pet.models import *

import debian.changelog

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm import exc

@view_config(route_name='overview', renderer='pet.web:templates/overview.pt')
def overview(request):
  return {'foo': 'bar'}

@view_config(route_name='changelog', renderer='pet.web:templates/changelog.pt')
def changelog(request):
  try:
    named_tree = request.session.query(NamedTree).filter_by(id=request.matchdict['named_tree_id']).one()
    changelog_contents = named_tree.file("debian/changelog").contents
    if changelog_contents is None:
      raise HTTPNotFound()
  except exc.NoResultFound:
    raise HTTPNotFound()

  changelog = debian.changelog.Changelog(changelog_contents, max_blocks=1, strict=False)
  return { "changelog": str(changelog) }