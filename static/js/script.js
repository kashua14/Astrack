function fileValidation(){
    var fileInput = document.getElementById('file');
    var filePath = fileInput.value;
    var allowedExtensions = /(\.csv)$/i;
    if(!allowedExtensions.exec(filePath)){
        document.getElementById('error').innerHTML = ' Only .csv files are allowed.'
        fileInput.value = '';
        return false;
    }else{
        document.getElementById('error').innerHTML = ''
    }
}