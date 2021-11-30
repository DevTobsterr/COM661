import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";



@Injectable()
export class WebService {
    constructor(public http: HttpClient, public Router: Router) {}

    list_of_posts: any;
    list_of_comments: any;

    getPosts(page: number) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/posts?pn='+ page)
    } 

    getPost(Post_ID: any) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_ID).toPromise()   
    }

    deletePost(Post_ID: any) {
        return this.http.delete('http://127.0.0.1:5000/api/v1.0/posts/' + Post_ID).toPromise()
    }

    updatePost(Post_Content: any, Post_ID: any) {
        let PostContent = new FormData();
        PostContent.append("Post_Author", Post_Content.Post_Author);
        PostContent.append("Post_Title", Post_Content.Post_Title);
        PostContent.append("Post_Body", Post_Content.Post_Body);
        PostContent.append("Post_Upvotes", Post_Content.Post_Upvotes);
        console.log(Post_Content);
        return this.http.put<any>('http://127.0.0.1:5000/api/v1.0/posts/' + Post_ID , PostContent).toPromise();
    }

    createPost(Post_Content: any) {
        let Post_Package = new FormData();
        Post_Package.append("Post_Author", Post_Content.Post_Author);
        Post_Package.append("Post_Title", Post_Content.Post_Title);
        Post_Package.append("Post_Body", Post_Content.Post_Body);
        return this.http.post<any>("http://127.0.0.1:5000/api/v1.0/posts", Post_Package).toPromise();
    }

    getComments(Post_UUID: any) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_UUID + "/comments").toPromise()   
    }

    getComment(Post_UUID: any, Comment_UUID: any) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_UUID + "/comments/" + Comment_UUID).toPromise()   
    }

    deleteComment(Post_UUID: any, Comment_UUID: any) {
        return this.http.delete('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_UUID + "/comments/" + Comment_UUID).toPromise()   


    } 

    createComment(Comment_Content: any, Post_UUID: any) {
        let Comment_Package = new FormData();
        Comment_Package.append("Comment_Author", Comment_Content.Comment_Author);
        Comment_Package.append("Comment_Body", Comment_Content.Comment_Body);
        return this.http.post<any>('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_UUID + "/comments", Comment_Package).toPromise();
    }
    
    updateComment(Post_Content: any, Post_UUID: any, Comment_UUID: any) {
        let Comment_Package = new FormData();
        Comment_Package.append("Comment_Author", Post_Content.Comment_Author);
        Comment_Package.append("Comment_Body", Post_Content.Comment_Body);
        console.log(Post_UUID, Comment_UUID)
        return this.http.put<any>('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_UUID + "/comments/" + Comment_UUID, Comment_Package).toPromise();
    } 

    upvotePost(Post_UUID: any) {
        return this.http.get<any>('http://127.0.0.1:5000/api/v1.0/post/upvote/'+ Post_UUID).toPromise();
    }















    getProfile(Post_Content: any) {
        let Username = new FormData();
        Username.append("Username", Post_Content.Username)
        return this.http.get("http://127.0.0.1:5000/api/v1.0/profile/"+ Username).toPromise();
    }


    

}


