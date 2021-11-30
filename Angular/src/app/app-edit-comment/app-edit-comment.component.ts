import { Route } from '@angular/compiler/src/core';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { WebService } from '../web.service';

@Component({
  selector: 'app-app-edit-comment',
  templateUrl: './app-edit-comment.component.html',
  styleUrls: ['./app-edit-comment.component.css']
})
export class AppEditCommentComponent implements OnInit {

  comment_update_submission_form: any;
  comment_information: any;

  constructor(private webservice: WebService, private route: ActivatedRoute ) { }
  
  onUpdate() {
    console.log("Temp")
  }

  async ngOnInit() {
    var Post_UUID: any = this.route.snapshot.params["Post_UUID"];
    var Comment_UUID: any = this.route.snapshot.params["Comment_UUID"];
    
    var comment_response = await this.webservice.getComment(Post_UUID, Comment_UUID);
    this.comment_information = comment_response;
    console.log(comment_response);

    
  }

}
