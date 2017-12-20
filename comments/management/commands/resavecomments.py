# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from comments.models import Comments

class Command(BaseCommand):
    # args = []
    def handle(self, *args, **options):
        comments = Comments.objects.filter()
        for item in comments:
            item.save()
            self.stdout.write('Successfully saved comment "%s"' % item.id)