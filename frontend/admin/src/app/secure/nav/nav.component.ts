import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { User } from '../../interfaces/user';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {
  @Input('user') user: User = null;
  constructor(
    private router: Router,
    private authService: AuthService
  
    ) { }

  ngOnInit() {
  }

  logout() {
    this.authService.logout().subscribe(
      res => {
        this.router.navigate(['/login']);
      }
    );
  }

}
