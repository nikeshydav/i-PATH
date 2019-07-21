<?php
error_reporting(1);

$missingdata = fopen("D:/RPAProject/iPath/untraced/missingdata.csv", "a+");

$fullurl = "https://trackthemissingchild.gov.in/trackchild/photograph_missing.php";

$urls[] = $fullurl;
echo "Curl ", $fullurl, " started. \n";

$post = http_build_query(['filter'=>'all', 'page'=>$argv[1], 'pagination'=>'pagination']);


$ch = curl_init();
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_FAILONERROR, 0);
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
curl_setopt($ch, CURLOPT_URL, $fullurl);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
// //curl_setopt($ch, CURLOPT_USERAGENT,'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13');
$returned = curl_exec($ch);
curl_close($ch);
echo "Curl ", $fullurl, " ended. \n";

// echo $returned;
$totalOccurence = substr_count($returned, ".photo_show");
if ($argv[1] == 1) {
    # code...
    $j = 1;
}else{
    $j = ($totalOccurence * ($argv[1] - 1)) + 1;
}


for ($i = $j; $i <= $j+$totalOccurence; $i++) {
    $wData = [];
    // echo $position1, "\n";
    if ($i == 0) {
        $position1 = stripos($returned, 'background-image: url("');
    } else {
        $position1 = stripos($returned, 'background-image: url("', $position2 + 300);
    }
    $position2 = stripos($returned, '");', $position1);

    // echo $position2, "\n";

    $length = $position2 - $position1 - 45;
    $img    = substr($returned, $position1 + 45, $length);

    $dataPostionTmp1 = stripos($returned, '<a href="javascript:void(0);" onclick="return match_show', $position2);
    $dataPostionTmp2 = stripos($returned, '<br/><a href="', $dataPostionTmp1);

    $dataTmp      = substr($returned, $dataPostionTmp1, $dataPostionTmp2 - $dataPostionTmp1);
    $dataPostion1 = stripos($dataTmp, 'value=\'');
    $dataPostion2 = stripos($dataTmp, '<br/><a href="', $dataPostion1);

    $data = substr($dataTmp, $dataPostion1 + 7, $dataPostion2 - $dataPostion1 - 5);
    
    $c = explode('|',$data);
    $c = implode(':',$c);
    // echo $data. "\n";
    // echo $c, "\n";
    $d = explode('<br/>', $c);

    $wData[0] = $i;
 
    foreach ($d as $key => $value) {
        $missingData            = explode(':', $value);
        $missingData[0]         = trim($missingData[0]);
        $missingData[1]         = trim($missingData[1]);
        $wData[$missingData[0]] = $missingData[1];
    }

    $wData = array_values($wData);

    // print_r($wData);
    fputcsv($missingdata, $wData, ",", '"');

    $file = fopen('D:/RPAProject/iPath/untraced/' . $i . '.jpg', 'w');
    fwrite($file, base64_decode($img));
    fclose($file);
    echo $i . ".jpg written \n";

}
fclose($missingdata);