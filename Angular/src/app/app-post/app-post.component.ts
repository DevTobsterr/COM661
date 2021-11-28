import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-app-post',
  templateUrl: './app-post.component.html',
  styleUrls: ['./app-post.component.css']
})
export class AppPostComponent implements OnInit {

  constructor(public webservice: WebService, private route: ActivatedRoute, public AuthenticationService: AuthService, private Router: Router) { }

  onDelete() {
    this.webservice.deletePost(this.route.snapshot.params["Post_ID"])
    this.Router.navigate(["/"])
  }

  async ngOnInit() {
    var response = await this.webservice.getPost(this.route.snapshot.params["Post_ID"]);
    console.log(response)
    this.list_of_posts = response;
  }
  
  list_of_posts: any = [];
   
}
