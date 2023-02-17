<table>
<thead>
<tr>
<th>Action or Event</th>
<th>Expected Result</th>
<th>Successful?<th>
</tr>
</thead>
<tbody>
<tr>
<td>Add paths to the URL as logged out user</td>
</tr>
<tr>
<td>

- path 'admin/',
- path 'api-auth/login/',
- path 'api-auth/logout/'
</td>
<td>Open the page with no errors and return the relevant data.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'profiles/',
- path 'profiles/<valid id>',
- path 'profiles/<invalid id>',
- path 'profiles/interests/',
- path 'profiles/interests/<valid id>'
- path 'profiles/interests/<invalid id>'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'categories/',
- path 'categories/genres/',
- path 'categories/<valid id>',
- path 'categories/<invalid id>',
- path 'categories/genres/<valid id>'
- path 'categories/genres/<invalid id>'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'events/',
- path 'events/<valid id>',
- path 'events/<invalid id>',
- path 'events/galleries/',
- path 'events/galleries/<valid id>',
- path 'events/galleries/<invalid id>',
- path 'events/galleries/photos',
- path 'events/galleries/photos/<valid id>',
- path 'events/galleries/photos/<invalid id>',
- path 'events/genres',
- path 'events/genres/<valid id>'
- path 'events/genres/<invalid id>'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>
    
- path 'interested/',
- path 'interested/<valid id>/',
- path 'interested/<invalid id>/',
- path 'going/',
- path 'going/<valid id>/',
- path 'going/<invalid id>/',
- path 'likes/',
- path 'likes/<valid id>/'
- path 'likes/<invalid id>/'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>    

- path 'comments/',
- path 'comments/<valid id>/'
- path 'comments/<invalid id>/'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>
    
- path 'followers/',
- path 'followers/<valid id>/'
- path 'followers/<invalid id>/'
</td>
<td>Open the page with no errors and return the relevant data.</td>
<td>Yes</td>
</tr>

<tr>
<td>Testing URLS paths as logged in user</td>
</tr>
<tr>
<td>

- path 'admin/',
- path 'api-auth/login/',
- path 'api-auth/logout/'
</td>
<td>Open the page with no errors and return the relevant data.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'profiles/',
- path 'profiles/<other user id>',
- path 'profiles/<invalid id>',
- path 'profiles/interests/',
- path 'profiles/interests/<other user id>'
- path 'profiles/interests/<invalid id>'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'profiles/<current user id>',
- path 'profiles/interests/<current user id>'
</td>
<td>Open the page with no errors and return the relevant data. The current user can update and delete their data.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'categories/',
- path 'categories/<valid id>',
- path 'categories/<invalid id>',
- path 'categories/genres/',
- path 'categories/genres/<valid id>'
- path 'categories/genres/<invalid id>'
</td>
<td>Open the page with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'categories/',
- path 'categories/genres/'
</td>
<td>If the logged in user is the admin retreive the relevant data, and enable update and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'categories/<valid id>',
- path 'categories/genres/<valid id>'
</td>
<td>If the logged in user is the admin retreive the relevant data, and enable update and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'events/<valid id>',
- path 'events/<invalid id>',
- path 'events/galleries/',
- path 'events/galleries/<valid id>',
- path 'events/galleries/<invalid id>',
- path 'events/galleries/photos/<valid id>',
- path 'events/galleries/photos/<invalid id>',
- path 'events/genres',
- path 'events/genres/<valid id>',
- path 'events/genres/<invalid id>'
</td>
<td>If the logged in user is not the event owner, nor the photos owner, open the pages with no errors and return the relevant data without create, update, and delete functionality.</td>
<td>Yes</td>
</tr>
<tr>
<td>
- path 'events/',
- path 'events/<invalid id>',
- path 'events/galleries/photos',
- path 'events/galleries/photos/<valid id>',
</td>
<td>Any logged in user can create events and add photos to others events. They can also update and delete their own photos.
They can also update and delete them.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'events/<invalid id>',
- path 'events/galleries/<invalid id>',
- path 'events/genres/<valid id>',
- path 'events/galleries/photos/<valid id>',
</td>
<td>If the logged in user is the event owner, they can update and delete the event, the genres, and their own photos.
The can also update the gallery, but not delete it or create it, since it creates automatically when the event is created.</td>
<td>Yes</td>
</tr>

<tr>
<td>
    
- path 'interested/',
- path 'interested/<valid id>/',
- path 'interested/<invalid id>/',
- path 'going/',
- path 'going/<valid id>/',
- path 'going/<invalid id>/',
- path 'likes/',
- path 'likes/<valid id>/'
- path 'likes/<invalid id>/'
</td>
<td>Any authenticated user can retrieve a list of interested, going and likes data. They can also show interest or go to an event. Any authenticated user can like a comment.</td>
<td>Yes</td>
</tr>
<tr>
<td>
    
- path 'interested/',
- path 'interested/<valid id>/',
- path 'interested/<invalid id>/',
- path 'going/',
- path 'going/<valid id>/',
- path 'going/<invalid id>/',
- path 'likes/',
- path 'likes/<valid id>/'
- path 'likes/<invalid id>/'
</td>
<td>If the logged in user is the owner of the interested, going and likes data, they can update and delete the data.</td>
<td>Yes</td>
</tr>
<tr>
<td>    

- path 'comments/',
- path 'comments/<valid id>/'
- path 'comments/<invalid id>/'
</td>
<td>Any authenticated user can retrieve and create comments.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'comments/<valid id>/'
</td>
<td>If the logged in user is the comment owner, they can also <td>Yes</td>
</tr>
<tr>
<td>
    
- path 'followers/',
- path 'followers/<valid id>/'
- path 'followers/<invalid id>/'
</td>
<td>Any authenticated user can view a list of followers and follow a profile.</td>
<td>Yes</td>
</tr>
<tr>
<td>

- path 'followers/<valid id>/'</td>
<td>If the logged in user is the owner of the follower data, they can delete it.</td>
<td>Yes</td>
</tr>