from typing import Type, List, Dict, Any

import dash

# deck related types
Card = List[str]
Fields = List[Dict[str, str]]
Content = Dict[str, Any]
Template = Dict[str, str]
Model = Dict[str, Any]
Media = List[Dict[str, Any]]
ModelDescription = (str, str, List[int], Model)

# preview related types
ElementInstance = dash.development.base_component.Component
Element = Type[ElementInstance]
