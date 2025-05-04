from django.core.management.base import BaseCommand
from blog.grpc.service import serve

class Command(BaseCommand):
    help = 'Run the gRPC server for PostService.'

    def handle(self, *args, **options):
        serve()
