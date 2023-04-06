import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { AuthGuard } from './auth.guard';
import { SigninComponent } from './signin/signin.component';


const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'signin', component: SigninComponent },
  { path: 'dashboard', component: DashboardComponent},
  { path: '', redirectTo: '/login', pathMatch: 'full' }
  // canActivate: [AuthGuard] 
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
    RouterModule.forChild([
      { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] }
    ])
  ],
  exports: [RouterModule]

})
export class AppRoutingModule { }
