import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '@auth0/auth0-angular';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-app-post',
  templateUrl: './app-post.component.html',
  styleUrls: ['./app-post.component.css']
})
export class AppPostComponent implements OnInit {

  constructor(public webservice: WebService, private route: ActivatedRoute, public AuthenticationService: AuthService, private Router: Router, private formBuilder: FormBuilder) { }


  list_of_posts: any = [];
  list_of_comments: any = [];
  CommentForm: any;
  

  onDeletePost() {
    this.webservice.deletePost(this.route.snapshot.params["Post_ID"])
    this.Router.navigate(["/"])
  }

  onDeleteComment(Comment_UUID: any) {
    var Post_UUID: any = this.route.snapshot.params["Post_ID"];
    this.webservice.deleteComment(Post_UUID, Comment_UUID);
    this.Router.navigate(["/"])

  }

  onCreateComment() {
    var Post_UUID: any = this.route.snapshot.params["Post_ID"];
    this.webservice.createComment(this.CommentForm.value, Post_UUID);
    this.Router.navigate(["/"])

  }

  async ngOnInit() {

    
    this.CommentForm = this.formBuilder.group({
      "Comment_Author": ["", Validators.required],
      "Comment_Body": ["", Validators.required]
    })

    var post_response = await this.webservice.getPost(this.route.snapshot.params["Post_ID"]);
    console.log(post_response)
    this.list_of_posts = post_response;

    var comment_response = await this.webservice.getComments(this.route.snapshot.params["Post_ID"])
    console.log(comment_response);
    this.list_of_comments = comment_response;


  }
  
}
