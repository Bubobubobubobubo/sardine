import pytest

from sardine_core import BaseHandler, FishBowl


def test_basic_children():
    group = BaseHandler()
    a = BaseHandler()
    b = BaseHandler()

    group.add_child(a)
    group.add_child(b)
    assert group.children == [a, b]
    assert a.parent is group and b.parent is group

    # no-ops
    group.add_child(a)
    group.remove_child(group)

    with pytest.raises(ValueError):
        group.add_child(group)

    group.remove_child(a)
    group.remove_child(b)
    assert group.children == []
    assert a.parent is None and b.parent is None


def test_child_locks():
    bowl = FishBowl()

    root = BaseHandler(lock_children=True)
    a = BaseHandler()
    a_a = BaseHandler()
    b = BaseHandler(lock_children=False)
    b_b = BaseHandler()
    handlers = (root, a, a_a, b, b_b)

    a.add_child(a_a)
    b.add_child(b_b)
    root.add_child(a)
    root.add_child(b)

    bowl.add_handler(root)
    bowl_handlers = bowl.handlers
    assert all(h in bowl_handlers for h in handlers)

    with pytest.raises(ValueError):
        bowl.remove_handler(a)

    with pytest.raises(ValueError):
        bowl.remove_handler(a_a)

    with pytest.raises(ValueError):
        bowl.remove_handler(b)

    bowl.remove_handler(b_b)

    bowl.remove_handler(root)
    bowl_handlers = bowl.handlers
    assert all(h not in bowl_handlers for h in handlers)
