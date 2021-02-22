import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../interfaces/user';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-secure',
  templateUrl: './secure.component.html',
  styleUrls: ['./secure.component.scss']
})
export class SecureComponent implements OnInit {
  user: User;
  constructor(
    private authServices: AuthService,
    private router: Router
  ) { }

  ngOnInit() {

    this.authServices.user().subscribe(
      (res: any) => {
        console.log(res.data);
        this.user = res.data;
      },
      err => {
        console.log(err);
        this.router.navigate(['/login']);
      }
    );
  }

}
