// Copyright 2012 Citrix Systems, Inc. Licensed under the
// Apache License, Version 2.0 (the "License"); you may not use this
// file except in compliance with the License.  Citrix Systems, Inc.
// reserves all rights not expressly granted by the License.
// You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Automatically generated by addcopyright.py at 04/03/2012
package com.cloud.agent.api;


public class ValidateSnapshotAnswer extends Answer {
    private String expectedSnapshotBackupUuid;
    private String actualSnapshotBackupUuid;
    private String actualSnapshotUuid;
    
    protected ValidateSnapshotAnswer() {
        
    }
    
    public ValidateSnapshotAnswer(ValidateSnapshotCommand cmd, boolean success, String result, String expectedSnapshotBackupUuid, String actualSnapshotBackupUuid, String actualSnapshotUuid) {
        super(cmd, success, result);
        this.expectedSnapshotBackupUuid = expectedSnapshotBackupUuid;
        this.actualSnapshotBackupUuid = actualSnapshotBackupUuid;
        this.actualSnapshotUuid = actualSnapshotUuid;
    }

    /**
     * @return the expectedSnapshotBackupUuid
     */
    public String getExpectedSnapshotBackupUuid() {
        return expectedSnapshotBackupUuid;
    }
    
    /**
     * @return the actualSnapshotBackupUuid
     */
    public String getActualSnapshotBackupUuid() {
        return actualSnapshotBackupUuid;
    }
    
    public String getActualSnapshotUuid() {
        return actualSnapshotUuid;
    }
}
