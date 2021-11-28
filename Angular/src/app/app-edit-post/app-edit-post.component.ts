import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { WebService } from '../web.service';

@Component({
  selector: 'app-app-edit-post',
  templateUrl: './app-edit-post.component.html',
  styleUrls: ['./app-edit-post.component.css']
})
export class AppEditPostComponent implements OnInit {

  blog_update_submission_form: any;
  list_of_posts: any = [];

  constructor(private webservice: WebService, private Router: ActivatedRoute, private router: Router, private formBuilder: FormBuilder) { }


  onUpdate() {
    this.webservice.updatePost(this.blog_update_submission_form.value);
    this.router.navigate(["/"]);
  }

  async ngOnInit() {

    var response = await this.webservice.getPost(this.Router.snapshot.params["Post_ID"]);
    this.list_of_posts = response;
    

    this.blog_update_submission_form = this.formBuilder.group({
      "Post_Author": ["", Validators.required],
      "Post_Title": ["", Validators.required],
      "Post_Body": ["", Validators.required],
      "Post_Upvotes": ["", Validators.required],
    })

   



  }


  
 
}
