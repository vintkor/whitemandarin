angular.module("main", [])
.controller("MyController", function($scope, $http, $sce) {
    $scope.afilter = {};
    $scope.aproperty = {};
    $scope.hotproperty = {};
    $scope.hotfilter = {};
    $scope.copyOk = false;

    $scope.updateCategory = function(key) {
        if ($scope.categoryId != "0"){
            var path = '/get_filters_properties/' + $scope.categoryId + '/';
            $scope.hotlineurl = false;
            $http.get(path).then(function(response){
                $scope.recheckfilters = false;
                $scope.recheckproperties = false;
                $scope.items = response.data.filters;
                $scope.pitems = response.data.properties;
                $scope.hotlineurl = response.data.hotlineurl;
                $scope.copyIsOk();
            });
        }
    }

    $scope.updateHotline = function(key) {

        if ($scope.hotlineId!="0"){

            var path = '/get_hotline_filters_properties/' + $scope.hotlineId + '/';

            $http.get(path).then(function(response){
                $scope.recheckhotfilters = false;
                $scope.recheckhotproperties = false;
                $scope.hotfilters = response.data.hotfilters;
                $scope.hotproperties = response.data.hotproperties;
            });
        }
    }

    $scope.deletePropertiesFilters = function(){

        var data = {
            'id': $scope.categoryId,
            'filters': $scope.afilter,
            'properties': $scope.aproperty,
        }

        // console.log(data);

        $http.post('/deletepropertiesfilters/', data).then(function(response){
            $scope.recheckfilters = false;
            $scope.recheckproperties = false;
            $scope.items = response.data.filters;
            $scope.pitems = response.data.properties;
        });

    }

    $scope.copyPropertiesFilters = function(){

        var data = {
            'cid': $scope.categoryId,
            'hid': $scope.hotlineId,
            'hotfilters': $scope.hotfilter,
            'hotproperties': $scope.hotproperty,
        }

        // console.log(data);

        $http.post('/copypropertiesfilters/', data).then(function(response){
            $scope.recheckfilters = false;
            $scope.recheckproperties = false;
            $scope.items = response.data.filters;
            $scope.pitems = response.data.properties;
        });


    }

    $scope.copyIsOk = function(){

        var oneproporfilter = false;
        $scope.copyOk = false;

        angular.forEach($scope.hotfilters, function(f){
            if ($scope.hotfilter[f._id.$oid]){
                oneproporfilter = true;
                return;
            }
        });

        if (!oneproporfilter){
            angular.forEach($scope.hotproperties, function(f){

                if ($scope.hotproperty[f._id.$oid]){
                    oneproporfilter = true;
                    return;
                }

            });

        }

        if (oneproporfilter && parseInt($scope.categoryId)){
            $scope.copyOk = true;
        }




    }



    $scope.$watch('recheckfilters', function() {

        angular.forEach($scope.items, function(f){

            $scope.afilter[f.id] = $scope.recheckfilters;

        });

     }, true);

    $scope.$watch('recheckproperties', function() {

        angular.forEach($scope.pitems, function(f){

            $scope.aproperty[f.id] = $scope.recheckproperties;

        });

     }, true);

    $scope.$watch('recheckhotfilters', function() {

        angular.forEach($scope.hotfilters, function(f){
            // console.log(f._id.$oid);

            $scope.hotfilter[f._id.$oid] = $scope.recheckhotfilters;

        });

     }, true);

   $scope.$watch('recheckhotproperties', function() {

        angular.forEach($scope.hotproperties, function(f){

            $scope.hotproperty[f._id.$oid] = $scope.recheckhotproperties;

        });

     }, true);

    $scope.$watch('hotfilter', function() {

        // console.log('we are here');

        $scope.copyIsOk();

     }, true);

   $scope.$watch('hotproperty', function() {

        $scope.copyIsOk();

     }, true);

} );
