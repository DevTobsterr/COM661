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



  isInvalid(control: any) {
    return this.CommentForm.controls[control].invalid && this.CommentForm.controls[control].touched;
  }

  isUntouched() {
    return this.CommentForm.controls.Comment_Author.pristine || this.CommentForm.controls.Comment_Body.pristine;
  }

  isIncomplete() {
    return this.isInvalid('Comment_Body') || this.isInvalid('Comment_Author') || this.isUntouched();
  }

  onDeletePost() {
    this.webservice.deletePost(this.route.snapshot.params["Post_ID"])
    this.Router.navigate(["/"])
  }

  onUpvote() {
    this.webservice.upvotePost(this.route.snapshot.params["Post_ID"]);
    // this.Router.navigate(["/"]);
  }

  onDeleteComment(Comment_UUID: any) {
    var Post_UUID: any = this.route.snapshot.params["Post_ID"];
    this.webservice.deleteComment(Post_UUID, Comment_UUID).subscribe((response: any) => {
      this.list_of_comments = this.webservice.getComments(this.route.snapshot.params["Post_ID"]);
    });

  }

  onCreateComment() {
    this.webservice.createComment(this.CommentForm.value, this.route.snapshot.params["Post_ID"]).subscribe((response : any) => {
      this.CommentForm.reset();
      this.list_of_comments = this.webservice.getComments(this.route.snapshot.params["Post_ID"]);
    });
  }

  ngOnInit() {

    this.list_of_comments = this.webservice.getComments(this.route.snapshot.params["Post_ID"]);
    this.list_of_posts = this.webservice.getPost(this.route.snapshot.params["Post_ID"]);


    this.CommentForm = this.formBuilder.group({
      "Comment_Author": ["", Validators.required],
      "Comment_Body": ["", Validators.required]
    })

  }

  list_of_posts: any = [];
  list_of_comments: any = [];
  CommentForm: any;


}
