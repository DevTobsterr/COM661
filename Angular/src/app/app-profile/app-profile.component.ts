import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { WebService } from '../web.service';

@Component({
  selector: 'app-app-profile',
  templateUrl: './app-profile.component.html',
  styleUrls: ['./app-profile.component.css']
})


export class AppProfileComponent implements OnInit {

  constructor(private webservice: WebService, private route: ActivatedRoute) { }

  async ngOnInit() {
    this.webservice.getProfile(this.route.snapshot.params["Username"]);
  }


}