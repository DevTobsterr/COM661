import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { FormBuilder, Validators } from '@angular/forms';
import { WebService } from '../web.service';


@Component({
  selector: 'app-app-login',
  templateUrl: './app-login.component.html',
  styleUrls: ['./app-login.component.css']
})


export class AppLoginComponent implements OnInit {

  constructor(public AuthenticationService: AuthService, private formBuilder: FormBuilder) { }


  login_form: any;

  onSubmit() {
    console.log(this.login_form.value);
  }


  ngOnInit(): void {
  
  }

}
