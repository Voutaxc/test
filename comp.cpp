#include <iostream>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
using namespace std;
 
string key[6]={"BEGIN","END","FOR","IF","THEN","ELSE"}; 
string outkey[7]={" LL","Begin","End","For","If","Then","Else"}; 
string letter[1000];

int length;
int num;
 
 
bool isNum(string s){
 if(s>="0" && s<="9")
  return true;
 return false;
}
 
bool isLetter(string s)
{
 if((s>="a" && s<="z")||(s>="A" && s<="Z"))
  return true;
 return false;
}
 
int isKey(string s){
 int i;
 for(i=0;i<6;i++){
  if(s==key[i])
  {
  	return i+1;
  	
  }
   
 }
 return 0;
}
 

string ident(string s,int n){
 int j=n+1;
 int flag=1;
 
 while(flag){
  if(isNum(letter[j]) || isLetter(letter[j])){
   s=(s+letter[j]).c_str();
   if(isKey(s)){
    j++;
    num=j;
    return s;
   }
   j++;
  }
  else{
   flag=0;
  }
 } 
 
 num=j;
 return s;
}
 

 
string Num(string s,int n){
 int j=n+1;
 int flag=1;
 
 while(flag){
  if(isNum(letter[j])){
   s=(s+letter[j]).c_str();
   j++;
  }
  else{
   flag=0;
  }
 }
 
 num=j;
 return s;
}
 
 
void TakeWord(){ 
 int k;
 
 for(num=0;num<length;)
 {
  string str1,str,st;
  str=letter[num];
  if(str=="$")
  {
  	  while(str=="$")
  {
  	 num++;
  	 str=letter[num];
  }
 
  }

 else if(isLetter(str))
{
    
     str1=ident(str,num);
     if(isKey(str1)!=0)
       cout<<outkey[isKey(str1)]<<endl;
     else
      cout<<"Ident("<<str1<<")"<<endl;
    continue;
    }
 
else if(isNum(str))
    {
    if(str=="0")
    {
    	while(str=="0"&&isNum(letter[num+1]))
    	{
    	num++;
    	str=letter[num];
		}
    	
	}
     str1=Num(str,num);
     cout<<"Int("<<str1<<")"<<endl;
    continue;
    }

	

else if(str==":")
	    {
	    	st=letter[num+1];
	    	if(st=="=")
	    	{
	    			cout<<"Assign"<<endl;
	    			num+=2;
			}
	    
	    	else
	    	{
	    			cout<<"Colon"<<endl;
	    			num++;
			}
	    
	    	
		}	
		else if(str=="+")
		{
			cout<<"Plus"<<endl;
			num++;
		}
		
	
		else if(str=="*")
		{
				cout<<"Star"<<endl;
				num++;
		}
	
		else if(str==",")
		{
			cout<<"Comma"<<endl;
			num++;
		}
		
		else if(str=="(")
		{
			cout<<"LParenthesis"<<endl;
			num++;
		}
		else if(str==")")
	     {
	     	cout<<"RParenthesis"<<endl;
	     	num++;
		 }
 else
 {
 	cout<<"Unknown"<<endl;
 	break;
 }
      
  }
 
 } 

 
int main(){
 char w;
 int i,j;
 freopen("input.txt","r",stdin);
 cin>>noskipws;

 length=0;
 while(cin>>w){
  if(w==' '||w=='\r\n'||w=='\t'||w=='\n'){
   letter[length]="$";
   length++;
  }
   else{
   letter[length]=w;
   length++;
  }
 }

 TakeWord();



 return 0;
}
