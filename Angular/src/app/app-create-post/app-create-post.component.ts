import { ThrowStmt } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '@auth0/auth0-angular';
import { WebService } from '../web.service';

@Component({
  selector: 'app-app-create-post',
  templateUrl: './app-create-post.component.html',
  styleUrls: ['./app-create-post.component.css']
})
export class AppCreatePostComponent implements OnInit {

  blog_submission_form: any;

  constructor(private webservice: WebService, private formBuilder: FormBuilder, public AuthenticationService: AuthService, private Router: Router) { }


  onSubmit() {
    this.webservice.createPost(this.blog_submission_form.value)
    this.Router.navigate(["/"])
  }

  ngOnInit(): void {
    this.blog_submission_form = this.formBuilder.group({
      "Post_Author": ["", Validators.required],
      "Post_Title": ["", Validators.required],
      "Post_Body": ["", Validators.required],
      
    })


  }

}
