/*
 *
 * django-codenerix-cms
 *
 * Codenerix GNU
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

 'use strict';
function Slider_calculate_price_discount(scope){
    var new_price = scope[scope.form_name]['SliderElementForm_new_price'].$viewValue;
    var old_price = scope[scope.form_name]["SliderElementForm_old_price"].$viewValue;
    var discount = scope[scope.form_name]["SliderElementForm_discount"].$viewValue;

    if (new_price != undefined && new_price != '' && !isNaN(new_price)){
        if (old_price != undefined && old_price != '' && !isNaN(old_price) && (discount == undefined || discount == '')){
            // discount
            var value = 100 - (new_price * 100 / old_price);
            var key = "SliderElementForm_discount";
        }else if (discount != undefined && discount != '' && !isNaN(discount) && (old_price == undefined || old_price == '')){
            // old_price
            var value = new_price * 100 / (100 - discount);
            var key = "SliderElementForm_old_price";
        }
        if (scope[scope.form_name][key] != undefined){
            scope[scope.form_name][key].$setViewValue(value.toString());
            scope[scope.form_name][key].$render();
        }
    }
}
function Slider_reset_field(scope, key){
    if (scope[scope.form_name][key] != undefined){
        scope[scope.form_name][key].$setViewValue('');
        scope[scope.form_name][key].$render();
    }
}


// Angular codenerix Controllers
angular.module('codenerixCMSControllers', [])

.controller('CDNXCMSFormSliderCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];

        $scope.change_price = function(){
            Slider_calculate_price_discount($scope);
        };
        $scope.change_discount = function(){
            Slider_calculate_price_discount($scope);
        };


        $scope.reset_discount = function(){
            Slider_reset_field($scope, "SliderElementForm_discount");
        };
        $scope.reset_oldprice = function(){
            Slider_reset_field($scope, "SliderElementForm_old_price");
        };
    }
]);
