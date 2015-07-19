# Django
from django.db.models.signals import post_save

# Project
from hierarchy.models import (School, fire_emis_metric_if_new)


class PostSaveHelper(object):
    """ Helper for managing post save hooks during tests. """

    def replace(self):
        """ Unhook post save hooks. """
        has_listeners = lambda: post_save.has_listeners(School)
        assert has_listeners(), (
            "School model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(fire_emis_metric_if_new, sender=School)
        assert not has_listeners(), (
            "School model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")


    def restore(self):
        """ Restore post save hooks. """
        has_listeners = lambda: post_save.has_listeners(School)
        assert not has_listeners(), (
            "School model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(fire_emis_metric_if_new, sender=School)
