import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';
import { AuthService } from '@auth0/auth0-angular';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-app-home',
  templateUrl: './app-home.component.html',
  styleUrls: ['./app-home.component.css']
})


export class AppHomeComponent implements OnInit {
  constructor(public webservice: WebService, public AuthenticationService: AuthService, private route: ActivatedRoute) { }

  PreviousPage() {
    if (this.page > 1) { 
      sessionStorage["page"] = this.page;
      this.page = this.page - 1; this.list_of_posts = this.webservice.getPosts(this.page);}
  }
  
  NextPage() {
      this.page = this.page + 1; 
      sessionStorage["page"] = this.page;
      this.list_of_posts = this.webservice.getPosts(this.page);
  }

  ngOnInit() {

    this.list_of_posts = this.webservice.getPosts(this.page);
    
  }

  list_of_posts: any = [];
  page: number = 1;

}
