from mariadmin.models import PostCategory, PostItem, PostComment
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import get_object_or_404

class PostTools:
    def getFeaturedPosts(self):
        featuredPosts = [
            {
                'heading': eachPost.postHeading,
                'image': eachPost.postHeadingImage,
                'date': eachPost.postDate.strftime("%b, %d, %Y"),
                'id': eachPost.pk
            } for eachPost in PostItem.objects.filter(postFeatured=True)
        ]

        return featuredPosts

    def confirmPostPresence(self, postId):
        # get status
        postObject = get_object_or_404(PostItem, pk=int(postId))

        foundStatus = True if postObject else False

        return foundStatus

    def getPostComments(self, postId, countWanted=False):
        # get the post object
        postObject = get_object_or_404(PostItem, pk=int(postId))

        # extract the comments for that post
        postComments = [
            {
                'name': eachComment.posterName,
                'comment': eachComment.postComment,
                'date': eachComment.commentDate.strftime("On %b, %d, %Y, At %H:%M %p")


            } for eachComment in PostComment.objects.filter(attachedPost=postObject)
        ]

        if countWanted is True:
            return len(postComments)

        else:
            return postComments

    def getPostCategories(self):
        categoryInformation = [
            {
                'name': eachCategory.categoryName,
                'id': eachCategory.pk
            } for eachCategory in PostCategory.objects.all()
        ]

        return categoryInformation


    def extractPostItemCategories(self, postCategoryData, isPreview=False):
        # extracting engine
        categoryExtractor = lambda categoryListString: categoryListString.split("#||#") if "#||#" in categoryListString else categoryListString

        # get the category
        presentCategories = categoryExtractor(postCategoryData)

        isCategoryList = False

        if isPreview is True:
            # determine if the object is a list
            isCategoryList = isinstance(presentCategories, list)

            presentCategories = presentCategories[0] if isCategoryList is True else presentCategories

        else:
            # needed for full display
            pass

        return presentCategories, isCategoryList

    def getSinglePostMeta(self, postId):
        # get the post item
        postItemSelected = get_object_or_404(PostItem, pk=int(postId))

        foundCategories, categoryStatus = self.extractPostItemCategories(postItemSelected.postPossibleCategories)

        # get single post data
        postData =  {
                'date': postItemSelected.postDate.strftime("%b. %d, %Y"),
                'heading': postItemSelected.postHeading,
                'heading_image': postItemSelected.postHeadingImage,
                'top_body': postItemSelected.postTopBody,
                'lower_body': postItemSelected.postLowerBody,
                'categories': foundCategories,
                'is_list': categoryStatus,
                'main_image': postItemSelected.postMainImage,
                'left_image': postItemSelected.postLeftSubImage,
                'right_image': postItemSelected.postRightSubImage,
                'featured': postItemSelected.postFeatured,
                'id': postItemSelected.pk

            }

        return postData

    def getFooterPosts(self, idToIgnore=None):
        # get posts that are not featured and also they dont have that id
        if idToIgnore is None:
            selectedPosts = PostItem.objects.filter(postFeatured=True)

        else:
            selectedPosts = PostItem.objects.exclude(pk=int(idToIgnore), postFeatured=True)

        # get the data
        if selectedPosts:
            # are for main
            resultForMain = True if idToIgnore is None else False

            # get the post's data
            extractedPostData = [
                self.generatePostPreview(eachSelectedPost, isForMain=resultForMain) for eachSelectedPost in selectedPosts
            ]

            postData = extractedPostData[:4] if len(extractedPostData) >= 4 else extractedPostData

        else:
            postData = []

        return postData

    def generatePostPreview(self, postItemObject, isForMain=False):
        # generate body preview
        bodyPreviewExtractor = lambda bodyData: (bodyData[:101] + "..") if len(bodyData) >= 100 else bodyData

        categoryInformation, _ = self.extractPostItemCategories(
            postCategoryData=postItemObject.postPossibleCategories,
                    isPreview=True)

        # prepare preview
        postPreviewData =  {
                'date': postItemObject.postDate.strftime("%b. %d, %Y"),
                'heading': postItemObject.postHeading,
                'heading_image': postItemObject.postHeadingImage,
                'body_preview': bodyPreviewExtractor(postItemObject.postTopBody),
                'category': categoryInformation,
                'id': postItemObject.pk

            }

        # add comments
        if isForMain is True:
            # get the comments
            postCommentsCount = PostTools().getPostComments(postId=postItemObject.pk, countWanted=True)

            # add the count to the object
            postPreviewData['comment_count'] = postCommentsCount

        else:
            # return the minimal preview
            pass


        return postPreviewData

    def getBlogPagePreviews(self):
        # prepare post previews
        postsPreview = [
            self.generatePostPreview(eachPostEntry) for eachPostEntry in PostItem.objects.all()
        ]

        return postsPreview


    def getAllPostsEntriesMeta(self):
        # prepare post entry data
        postsInformation = [
            self.getSinglePostMeta(eachPostEntry.pk) for eachPostEntry in PostItem.objects.all()
        ]

        return postsInformation




    def getPostMetaPreview(self):
        postsPreview = [
            {
                'date': eachPostEntry.postDate.strftime("%d-%m-%Y, %H:%M %p"),
                'featured': eachPostEntry.postFeatured,
                'id': eachPostEntry.pk

            } for eachPostEntry in PostItem.objects.all()
        ]

        return postsPreview

class PostsManager:
    def __init__(self, request:HttpRequest):
        # access the request
        self.requestObject = request

        # access the request data
        self.sentRequestData = request.POST.dict()

    def updatePostItemState(self):
        # get the id
        postId = self.sentRequestData['post-id']

        postState = True if self.sentRequestData['featured-state'] == 'true' else False

        # get the selected object
        selectedPostItem = PostItem.objects.get(pk=postId)

        # update its state
        selectedPostItem.postFeatured = postState

        # save the changes
        selectedPostItem.save()

        return

    def postMetaApi(self):
        # id of post
        requestedPostId = self.sentRequestData['post-id']

        # get the data
        neededPostData = PostTools().getSinglePostMeta(postId=requestedPostId)

        return neededPostData




    def getPostItemViaId(self, postItemId):
        """
        Retrieves a post item via its id or pk
        """
        # get the object
        neededPostItem = get_object_or_404(PostItem, pk=postItemId)

        return neededPostItem


    def savePostComment(self):
        postId = self.sentRequestData['post-id']

        posterName = self.sentRequestData['poster-name'].title()

        postComment = self.sentRequestData['poster-comment'].capitalize()

        # get the post
        attachedPost = get_object_or_404(PostItem, pk=postId)


        # create a post instance
        commentInstance = PostComment.objects.create(
            attachedPost=attachedPost,
            posterName=posterName,
            postComment=postComment)

        # save the post
        commentInstance.save()

        return postId







    def createOrUpdatePostItem(self, operationType):
        """
            Will create or update a post item
            1 - new, 2 - edit
        """
        # post item
        newPost = PostItem.objects.create() if operationType == 1 else self.getPostItemViaId(self.sentRequestData['edited-post'])

        # get the heading
        postHeading = self.sentRequestData['post-heading'].capitalize()

        # save the post
        postHeadingImage = self.sentRequestData['selected-header-image']

        # get the top body
        postTopBody = self.sentRequestData['post-top-body']

        # main image
        postMainImage = self.sentRequestData['main-post-image']

        # get lower body
        postLowerBody = self.sentRequestData['post-lower-body']

        # get all tags
        applicableTags = [
            eachKey for eachKey, eachValue in self.sentRequestData.items() if eachValue == 'on'
        ]


        # get applicable tags
        postCategories = '#||#'.join(sorted(applicableTags)) if len(applicableTags) > 0 else 'general'


        # add details
        newPost.postHeading = postHeading

        # heading image
        newPost.postHeadingImage = postHeadingImage

        # top body
        newPost.postTopBody = postTopBody

        # main image
        newPost.postMainImage = postMainImage

        # add sub images
        if 'left-sub-image' in  self.sentRequestData:
            newPost.postLeftSubImage = self.sentRequestData['left-sub-image']


        if 'right-sub-image' in  self.sentRequestData:
            newPost.postRightSubImage = self.sentRequestData['right-sub-image']

        # add lower body
        newPost.postLowerBody = postLowerBody


        # categories
        newPost.postPossibleCategories = postCategories

        # save the post
        newPost.save()

        return



    def savePostItem(self):
        # debug
        # {'post-heading': 'hello', 'selected-header-image': '/assets/36390a11-1f12-4224-8b1c-db19ccec879a.jpeg',
        # 'post-top-body': 'hello here', 'main-post-image': '/assets/36390a11-1f12-4224-8b1c-db19ccec879a.jpeg',
        # 'left-sub-image': '', 'right-sub-image': '', 'Business': 'on', 'Adventure': 'on'}
        # print("received:", self.sentRequestData)

        # get the heading
        postHeading = self.sentRequestData['post-heading'].capitalize()

        # check if its an edit
        if 'edited-post' in self.sentRequestData:
            # get the item id
            postItemId = self.sentRequestData['edited-post']

            # debug
            # print("Post id:", postItemId, " Type:", type(postItemId))

            # check if the heading does not exist anywhere else
            headingDuplicate = PostItem.objects.exclude(pk=postItemId).filter(postHeading=postHeading).first()

            # debug
            # print("Found:", headingDuplicate.count())

            if headingDuplicate:
                # alert duplicate
                messages.success(self.requestObject, 'The post item was exits already maybe change the heading!')

            else:
                # perform the edit
                self.createOrUpdatePostItem(2)

                # alert success
                messages.success(self.requestObject, 'The post item was updated successfully!')


        else:
            # determine if its a duplicate
            isDuplicate = PostItem.objects.filter(postHeading=postHeading).first()

            if isDuplicate:
                # alert
                messages.warning(self.requestObject, 'The post name already exists please try using a different one!')

            else:
                # save the post as new
                self.createOrUpdatePostItem(1)

                # alert success
                messages.success(self.requestObject, 'The post item was saved successfully!')


        return

    def deleteAllPostComments(self, postId):
        # get the post item
        postItemWithComments = get_object_or_404(PostItem, pk=postId)

        # get all the comments
        allComments = postItemWithComments.associated_comments.all()

        # delete the post
        allComments.delete()

        # alert success
        messages.success(self.requestObject, "All Post Comments were deleted successfully!")

        return


    def deletePostCategory(self, categoryId):
        # delete the post
        postCategoryObject = get_object_or_404(PostCategory, pk=categoryId)

        # delete the post
        postCategoryObject.delete()

        messages.success(self.requestObject, "Post category was deleted successfully!")

        return



    def deletePostItem(self, postItemId):
        # delete the post item
        postItemObject = get_object_or_404(PostItem, pk=postItemId)

        # delete the post
        postItemObject.delete()

        messages.success(self.requestObject, "The Post and it comments were deleted successfully!")

        return

    def saveCategoryInformation(self):
        # get the category name and validate its existance
        referenceCategoryName = self.sentRequestData['post-category-name'].title()

        # check for duplicates
        isDuplicate = PostCategory.objects.filter(categoryName=referenceCategoryName).first()

        if isDuplicate:
            # alert duplicate
            messages.warning(self.requestObject, "Category name already exists, maybe delete it first!")

        else:
            # create new category
            newCategory = PostCategory.objects.create(categoryName=referenceCategoryName)

            # save
            newCategory.save()

            messages.success(self.requestObject, f"Category '{referenceCategoryName}' was saved successfully! !")


        return

