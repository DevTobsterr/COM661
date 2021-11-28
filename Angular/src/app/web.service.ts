import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";



@Injectable()
export class WebService {
    constructor(public http: HttpClient, public Router: Router) {}

    list_of_posts: any;

    getPosts(page: number) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/posts?pn='+ page)
    } 

    getPost(Post_ID: any) {
        return this.http.get('http://127.0.0.1:5000/api/v1.0/posts/'+ Post_ID).toPromise()   
    }

    deletePost(Post_ID: any) {
        return this.http.delete('http://127.0.0.1:5000/api/v1.0/posts/' + Post_ID).toPromise()
    }

    updatePost(Post_Content: any) {
        let PostContent = new FormData();
        PostContent.append("Post_Author", Post_Content.Post_Author);
        PostContent.append("Post_Title", Post_Content.Post_Title);
        PostContent.append("Post_Body", Post_Content.Post_Body);
        PostContent.append("Post_Upvotes", Post_Content.Post_Upvotes);
        console.log(Post_Content)
        return this.http.put<any>('http://127.0.0.1:5000/api/v1.0/posts/', PostContent).toPromise();
    }

    createPost(Post_Content: any) {
        let PostContent = new FormData();
        PostContent.append("Post_Author", Post_Content.Post_Author);
        PostContent.append("Post_Title", Post_Content.Post_Title);
        PostContent.append("Post_Body", Post_Content.Post_Body);
        return this.http.post("http://127.0.0.1:5000/api/v1.0/posts", PostContent).toPromise();
    }


    getProfile(User_ID: any) {
        return this.http.get("http://127.0.0.1:5000/api/v1.0/profile/"+ User_ID).toPromise();
    }


    

}


