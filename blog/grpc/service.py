import grpc
from concurrent import futures
from django.contrib.auth import get_user_model
from blog.grpc.post_pb2 import (
    Post as PostMessage,
    GetPostResponse,
    CreatePostResponse,
)
from blog.grpc.post_pb2_grpc import PostServiceServicer, add_PostServiceServicer_to_server
from blog.models import Post

User = get_user_model()

def _post_to_message(post: Post) -> PostMessage:
    return PostMessage(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author.id,
        category=post.category.id
    )



class PostService(PostServiceServicer):
    def GetPost(self, request, context):
        try:
            post = Post.objects.get(id=request.id)
        except Post.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Post with id={request.id} not found")
            return GetPostResponse()  # empty
        return GetPostResponse(post=_post_to_message(post))

    def CreatePost(self, request, context):
        post = Post.objects.create(
            title=request.title,
            content=request.content,
            author_id=request.author,
            category_id=request.category
        )
        return CreatePostResponse(post=_post_to_message(post))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_PostServiceServicer_to_server(PostService(),server)
    server.add_insecure_port('[::]:50052')
    print("gRPC PostService listening on port 50052…")
    server.start()
    server.wait_for_termination()
